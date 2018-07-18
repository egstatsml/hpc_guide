#!/usr/bin/env Rscript

# breast_cancer_bt.R
#
# Simple script that will use boosted regression trees
# to predict the presence of breast cancer based on 
# biopsy information
#
# The script can be invoked with
#  Rscript breast_cancer_bt.R --ntrees <number_of_trees>
# 
# By default, the number of trees is set to 10000, and will
# be set to this value if you don't specify it 
#
# Author:
#  Ethan Goan - ej.goan@qut.edu.au
#
# Licence:
#  MIT

#load in the libraries we are using
library('mlbench')
library('gbm')
library("optparse")

#load in the dataframe
data("BreastCancer")

parseArgs <- function(){
  # Parses in command line arguments
  #
  # Args:
  #   NA
  #
  # Returns:
  #   Dataframe with the columns ntrees filled with
  #   value supplied by the command line
  #Load in the arguments from the command line
  option_list = list(
    make_option(c("-n", "--ntrees"), type="integer", default=10000, 
                help="number of trees")); 
  opt_parser = OptionParser(option_list=option_list);
  args = parse_args(opt_parser);
  return(args)
}




test_bt <- function(bt.model, test_data){
  # Will test the accuracy of the fitted model
  # on the specified training set
  #
  # Args:
  #   bt.model: Boosted tree model from gbm that
  #   was fit on the training data
  #   test_data: dataframe containing the test data
  #
  # Returns:
  #   Dataframe with the columns for accuracy, sensitivity
  #   and specificity
  print('begin testing')
  #run the test data through the model
  predicted <- predict(bt.model, test_data, n.trees = 10000, type = "response")
  #threshold the output
  predicted[predicted < 0.5] = 0
  predicted[predicted > 0.5] = 1
  summ <- summarise_prediction(predicted, test_data)
  return(summ)
}


summarise_prediction <- function(predicted, test_data){
  # Will summarise the prediction performance
  # of the fitted model
  #
  # Args:
  #   predicted: Thresholded (binary) output of the model
  #   test_data: dataframe containing the test data
  #
  # Returns:
  #   list with the accuracy, sensitivity and specificity
  #   of our models prediction
  #

  
  # predicted is the output of the model
  # data is the ground truth data base for test data
  tp <- sum((predicted == 1) & (test_data$Class.bin == 1))
  fp <- sum((predicted == 1) & (test_data$Class.bin == 0))
  tn <- sum((predicted == 0) & (test_data$Class.bin == 0))
  fn <- sum((predicted == 0) & (test_data$Class.bin == 1))
  
  acc <- (tp + tn) / (nrow(test_data))
  sens <- tp / (tp + fn)
  spec <- tn / (tn + fp)
  return(list("acc" = acc, "sens" = sens, "spec" = spec ))
}



print_test_summary <- function(summ, ntrees){
  # Will print some summary info for us
  #
  # Args:
  #   summ: the summary list that holds our models
  #   performance
  #   ntrees: The number of trees that was specified by the
  #   command line
  #
  # Returns:
  #   NA
  print("Testing Results")
  print(sprintf("Boosted Regression Trees Model with %d trees", ntrees))
  print(sprintf("acc  = %f", summ$acc))
  print(sprintf("sens = %f", summ$sens))
  print(sprintf("spec = %f", summ$spec))
  print(":)")
  }

main <- function(){
  # Main function that is invoked by the script
  # I write my R code like this to avoid having lots
  # of global variables that I don't want/need
  #
  # Args:
  #  NA
  # Returns:
  #  NA

  #parse in the command line args
  args <- parseArgs()
  #convert the dataset class labels to binary values
  #malignant = 1, benign = 0
  BreastCancer$Class.bin <- 0
  BreastCancer$Class.bin[BreastCancer$Class=="malignant"]  <- 1
  #split the data set
  BreastTrain <- BreastCancer[0:500,]
  BreastTest <- BreastCancer[500:nrow(BreastCancer),]
  #now lets fit the model
  bt <- gbm(Class.bin~Bare.nuclei+Bl.cromatin+Normal.nucleoli+Mitoses,
         data=BreastTrain,
         distribution = "bernoulli",
         interaction.depth=3,
         bag.fraction=0.7,
         n.trees = args$ntrees)
  #lets see how well our model fits to the test data
  summ <- test_bt(bt, BreastTest)
  #print the summary results
  print_test_summary(summ, args$ntrees)
}

#invoke the main function
main()

