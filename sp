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
    "CheckJobStatus1": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.RunGlueJob1.Status",
          "StringEquals": "SUCCEEDED",
          "Next": "CheckJobStatus2"
        }
      ],
      "Default": "WaitForCompletion"
    },
    "CheckJobStatus2": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.RunGlueJob2.Status",
          "StringEquals": "SUCCEEDED",
          "Next": "ParallelExecutionSucceeded"
        }
      ],
      "Default": "WaitForCompletion"
    },
    "WaitForCompletion": {
      "Type": "Wait",
      "Seconds": 300,
      "SecondsPath": "$.WaitTime",
      "Next": "CheckTotalWaitTime"
    },
    "CheckTotalWaitTime": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.WaitTime",
          "NumericEquals": 720,
          "Next": "ParallelFailed"
        },
        {
          "Variable": "$.WaitTime",
          "NumericLessThan": 720,
          "Next": "WaitForCompletion"
        }
      ],
      "Default": "ParallelFailed"
    },
    "ParallelFailed": {
      "Type": "Fail",
      "Cause": "One or more parallel Glue jobs failed",
      "Error": "ParallelGlueJobFailure"
    },
    "ParallelExecutionSucceeded": {
      "Type": "Succeed",
      "End": true
    },
    "TerminalState": {
      "Type": "Succeed"
    }
  }
}
