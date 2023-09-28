{
  "StartAt": "ParallelExecution",
  "States": {
    "ParallelExecution": {
      "Type": "Parallel",
      "Branches": [
        {
          "StartAt": "RunGlueJob1",
          "States": {
            "RunGlueJob1": {
              "Type": "Task",
              "Resource": "arn:aws:states:::glue:startJobRun.sync",
              "Parameters": {
                "JobName": "YourGlueJobName",
                "Arguments": {
                  "--input_json": "s3://your-bucket/json-file-1.json"
                }
              },
              "End": true
            }
          }
        },
        {
          "StartAt": "RunGlueJob2",
          "States": {
            "RunGlueJob2": {
              "Type": "Task",
              "Resource": "arn:aws:states:::glue:startJobRun.sync",
              "Parameters": {
                "JobName": "YourGlueJobName",
                "Arguments": {
                  "--input_json": "s3://your-bucket/json-file-2.json"
                }
              },
              "End": true
            }
          }
        },
        {
          "StartAt": "RunGlueJob3",
          "States": {
            "RunGlueJob3": {
              "Type": "Task",
              "Resource": "arn:aws:states:::glue:startJobRun.sync",
              "Parameters": {
                "JobName": "YourGlueJobName",
                "Arguments": {
                  "--input_json": "s3://your-bucket/json-file-3.json"
                }
              },
              "End": true
            }
          }
        },
        {
          "StartAt": "RunGlueJob4",
          "States": {
            "RunGlueJob4": {
              "Type": "Task",
              "Resource": "arn:aws:states:::glue:startJobRun.sync",
              "Parameters": {
                "JobName": "YourGlueJobName",
                "Arguments": {
                  "--input_json": "s3://your-bucket/json-file-4.json"
                }
              },
              "End": true
            }
          }
        },
        {
          "StartAt": "RunGlueJob5",
          "States": {
            "RunGlueJob5": {
              "Type": "Task",
              "Resource": "arn:aws:states:::glue:startJobRun.sync",
              "Parameters": {
                "JobName": "YourGlueJobName",
                "Arguments": {
                  "--input_json": "s3://your-bucket/json-file-5.json"
                }
              },
              "End": true
            }
          }
        }
      ],
      "End": true
    },
    "CheckJobStatus": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.RunGlueJob1.Status",
          "StringEquals": "SUCCEEDED",
          "Next": "CheckJob2Status"
        },
        {
          "Variable": "$.RunGlueJob2.Status",
          "StringEquals": "SUCCEEDED",
          "Next": "CheckJob3Status"
        },
        {
          "Variable": "$.RunGlueJob3.Status",
          "StringEquals": "SUCCEEDED",
          "Next": "CheckJob4Status"
        },
        {
          "Variable": "$.RunGlueJob4.Status",
          "StringEquals": "SUCCEEDED",
          "Next": "CheckJob5Status"
        },
        {
          "Variable": "$.RunGlueJob5.Status",
          "StringEquals": "SUCCEEDED",
          "Next": "MainJob"
        }
      ],
      "Default": "ParallelFailed" // If none of the jobs succeeded, go to the failure path
    },
    "CheckJob2Status": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.RunGlueJob2.Status",
          "StringEquals": "SUCCEEDED",
          "Next": "CheckJob3Status"
        },
        {
          "Variable": "$.RunGlueJob2.Status",
          "StringEquals": "FAILED",
          "Next": "ParallelFailed" // If job 2 failed, go to the failure path
        },
        {
          "Variable": "$.RunGlueJob2.Status",
          "StringEquals": "SUCCEEDED",
          "Next": "MainJob"
        }
      ],
      "Default": "ParallelFailed"
    },
    "CheckJob3Status": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.RunGlueJob3.Status",
          "StringEquals": "SUCCEEDED",
          "Next": "CheckJob4Status"
        },
        {
          "Variable": "$.RunGlueJob3.Status",
          "StringEquals": "FAILED",
          "Next": "ParallelFailed" // If job 3 failed, go to the failure path
        },
        {
          "Variable": "$.RunGlueJob3.Status",
          "StringEquals": "SUCCEEDED",
          "Next": "MainJob"
        }
      ],
      "Default": "ParallelFailed"
    },
    "CheckJob4Status": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.RunGlueJob4.Status",
          "StringEquals": "SUCCEEDED",
          "Next": "CheckJob5Status"
        },
        {
          "Variable": "$.RunGlueJob4.Status",
          "StringEquals": "FAILED",
          "Next": "ParallelFailed" // If job 4 failed, go to the failure path
        },
        {
          "Variable": "$.RunGlueJob4.Status",
          "StringEquals": "SUCCEEDED",
          "Next": "MainJob"
        }
      ],
      "Default": "ParallelFailed"
    },
    "CheckJob5Status": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.RunGlueJob5.Status",
          "StringEquals": "SUCCEEDED",
          "Next": "MainJob"
        },
        {
          "Variable": "$.RunGlueJob5.Status",
          "StringEquals": "FAILED",
          "Next": "ParallelFailed" // If job 5 failed, go to the failure path
        }
      ],
      "Default": "ParallelFailed"
    },
    "MainJob": {
      "Type": "Task",
      "Resource": "arn:aws:states:::glue:startJobRun.sync",
      "Parameters": {
        "JobName": "YourMainGlueJobName",
        "Arguments": {
          "--input_json": "s3://your-bucket/main-input.json" // Provide the input for the main Glue job
        }
      },
      "End": true,
      "Catch": [
        {
          "ErrorEquals": ["States.ALL"],
          "Next": "ErrorHandlingMain" // Transition to error handling state for any error in the main Glue job
        }
      ]
    },
    "ErrorHandlingMain": {
      "Type": "Fail",
      "Cause": "Main Glue job failed",
      "Error": "MainGlueJobFailure"
    },
    "ParallelFailed": {
      "Type": "Fail",
      "Cause": "One or more parallel Glue jobs failed",
      "Error": "ParallelGlueJobFailure"
    },
    "ErrorHandling": {
      "Type": "Fail",
      "Cause": "One or more Glue jobs failed",
      "Error": "GlueJobFailure"
    },
    "TerminalState": {
      "Type": "Succeed" // This state marks the successful completion of the state machine
    }
  }
}
