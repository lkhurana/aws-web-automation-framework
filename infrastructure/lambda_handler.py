import logging
import json
import boto3
import time

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

ssm_client = boto3.client('ssm')
ec2_client = boto3.client('ec2')

def lambda_handler(event, context):
    """
    Lambda function to ensure EC2 instance is running, execute the main script, and stop the instance afterward.
    """
    logger.info("Lambda function started")
    INSTANCE_ID = 'i-08082bcb39ef4fa33'
    RUN_COMMAND = 'bash -c "cd /home/ubuntu/projects/aws-web-automation-framework/ && source aws-web-auto-env/bin/activate && python -m src.main && exit 0"'
    
    try:
        
        # Wait for instance to be running
        for _ in range(18):  # Check every 10 seconds, up to 3 minutes
            # Check if the instance is running
            response = ec2_client.describe_instances(InstanceIds=[INSTANCE_ID])
            state = response['Reservations'][0]['Instances'][0]['State']['Name']

            if state == 'stopped':
                logger.info(f"Instance {INSTANCE_ID} is stopped. Starting it now.")
                ec2_client.start_instances(InstanceIds=[INSTANCE_ID])
                time.sleep(10)
            elif state == 'running':
                logger.info(f"Instance {INSTANCE_ID} is now running.")
                break
            else:
                logger.info(f"Instance {INSTANCE_ID} is {state}. Waiting for the state to change.")
            time.sleep(10)
        else:
            raise Exception(f"Instance {INSTANCE_ID} did not start within the expected time.")
        
        time.sleep(10)
        logger.info('Sending command')
        # Use SSM to send a command to the instance to run the Python script
        response = ssm_client.send_command(
            InstanceIds=[INSTANCE_ID],
            DocumentName="AWS-RunShellScript",
            Parameters={'commands': [RUN_COMMAND]},
            TimeoutSeconds=600
        )
        logger.info(f'SSM command sent to EC2 instance {INSTANCE_ID}')
        logger.info(f'SSM command response: {response}')
        
        # Log command ID
        command_id = response['Command']['CommandId']
        logger.info(f"Command sent. Command ID: {command_id}")
        
        # Wait for the command to complete
        time.sleep(10)  # Initial pause before checking status
        command_status = "InProgress"
        while command_status in ["Pending", "InProgress"]:
            command_invocation = ssm_client.get_command_invocation(
                CommandId=command_id,
                InstanceId=INSTANCE_ID
            )
            command_status = command_invocation['Status']
            logger.info(f"Command status: {command_status}")
            time.sleep(5)  # Check every 5 seconds

        # Stop the instance after the command is complete
        if command_status == "Success":
            logger.info(f"Command completed successfully. Stopping instance {INSTANCE_ID}.")
            ec2_client.stop_instances(InstanceIds=[INSTANCE_ID])
            logger.info(f"Instance {INSTANCE_ID} has been stopped.")
            time.sleep(10)
        else:
            logger.info(f"Command did not complete successfully: {command_status}")
        
        return {
            'statusCode': 200 if command_status == "Success" else 500,
            'body': {
                "command_id": command_id,
                "status": command_status
            }
        }
        
    except Exception as e:
        logger.info(f"Failed to send command to EC2 instance: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }