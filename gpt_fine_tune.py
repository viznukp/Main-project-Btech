import os
from openai import OpenAI
import time
import sys

client = OpenAI(
  api_key='',
)



training_file_id = client.files.create(
  file=open("gpt_training_data7.jsonl", "rb"),
  purpose="fine-tune"
)

# validation_file_id = client.files.create(
#   file=open(validation_file_name, "rb"),
#   purpose="fine-tune"
# )

print(f"Training File ID: {training_file_id}")
# print(f"Validation File ID: {validation_file_id}")


response = client.fine_tuning.jobs.create(
  training_file=training_file_id.id, 
  # validation_file=validation_file_id.id,
  model="gpt-3.5-turbo", 
  hyperparameters={
    "n_epochs": 3,
	  # "batch_size": 3,
	  # "learning_rate_multiplier": 0.3
  }
)
job_id = response.id
status = response.status

print(f'Fine-tunning model with jobID: {job_id}.')
print(f"Training Response: {response}")
print(f"Training Status: {status}")



status = client.fine_tuning.jobs.retrieve(job_id).status
if status not in ["succeeded", "failed"]:
    print(f"Job not in terminal status: {status}. Waiting.")
    while status not in ["succeeded", "failed"]:
        time.sleep(2)
        status = client.fine_tuning.jobs.retrieve(job_id).status
        print(f"Status: {status}")
else:
    print(f"Finetune job {job_id} finished with status: {status}")
print("Checking other finetune jobs in the subscription.")
result = client.fine_tuning.jobs.list()
print(f"Found {len(result.data)} finetune jobs.")

if status == "failed":
  job_details = client.fine_tuning.jobs.retrieve(job_id)
  error_message = job_details.error_message
  print(f"Error message: {error_message}")

# Retrieve the finetuned model
fine_tuned_model = result.data[0].fine_tuned_model
print(fine_tuned_model)

