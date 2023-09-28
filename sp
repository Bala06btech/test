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
        }
      ],
      "End": true
    },
    "CheckGlueJob1Status": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.RunGlueJob1.Status",
          "StringEquals": "SUCCEEDED",
          "Next": "MainJob"
        },
        {
          "Variable": "$.RunGlueJob1.Status",
          "StringEquals": "FAILED",
          "Next": "GlueJob1Failed"
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
    "GlueJob1Failed": {
      "Type": "Fail",
      "Cause": "GlueJob1 failed",
      "Error": "GlueJob1Failure"
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
