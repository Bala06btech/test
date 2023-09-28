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
    "CheckParallelStatus": {
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
      "End": true
    },
    "ParallelFailed": {
      "Type": "Fail",
      "Cause": "One or more parallel Glue jobs failed",
      "Error": "ParallelGlueJobFailure"
    },
    "TerminalState": {
      "Type": "Succeed" // This state marks the successful completion of the state machine
    }
  }
}
