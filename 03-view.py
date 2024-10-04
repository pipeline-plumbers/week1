import boto3
import schedule
import time

# Initialize EC2 client
region_name = 'us-east-1'
ec2_client = boto3.client('ec2', region_name=region_name)

# Load volume_id from file
def load_volume_id():
    with open('instance_volume_data.txt', 'r') as file:
        for line in file:
            if line.startswith('volume_id'):
                return line.strip().split('=')[1]

def create_volume_snapshots():
    volume_id = load_volume_id()
    response = ec2_client.create_snapshot(VolumeId=volume_id)
    print(f"Snapshot created for Volume ID: {volume_id} - Snapshot ID: {response['SnapshotId']}")

def create_immediate_snapshot():
    volume_id = load_volume_id()
    response = ec2_client.create_snapshot(VolumeId=volume_id)
    print(f"Immediate snapshot created for Volume ID: {volume_id} - Snapshot ID: {response['SnapshotId']}")

# Schedule to run daily at midnight
schedule.every().day.at("00:00").do(create_volume_snapshots)

if __name__ == "__main__":
    # Create an immediate snapshot
    create_immediate_snapshot()

    # Schedule daily snapshot backups
    while True:
        schedule.run_pending()
        time.sleep(60)
