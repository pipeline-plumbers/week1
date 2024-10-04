import boto3
import operator

# Initialize EC2 client
region_name = 'us-east-1'
ec2_client = boto3.client('ec2', region_name=region_name)

# Load volume_id from file
def load_volume_id():
    with open('instance_volume_data.txt', 'r') as file:
        for line in file:
            if line.startswith('volume_id'):
                return line.strip().split('=')[1]

def get_snapshots_for_volume(volume_id):
    snapshots = ec2_client.describe_snapshots(
        Filters=[{'Name': 'volume-id', 'Values': [volume_id]}, {'Name': 'owner-id', 'Values': ['self']}]
    )
    return snapshots['Snapshots']

def sort_snapshots_by_date(snapshots):
    return sorted(snapshots, key=operator.itemgetter('StartTime'), reverse=True)

def delete_old_snapshots(sorted_snapshots):
    for snapshot in sorted_snapshots[2:]:  # Keep only two most recent snapshots
        print(f"Deleting snapshot {snapshot['SnapshotId']} created on {snapshot['StartTime']}")
        ec2_client.delete_snapshot(SnapshotId=snapshot['SnapshotId'])

def cleanup_snapshots():
    volume_id = load_volume_id()
    snapshots = get_snapshots_for_volume(volume_id)
    if len(snapshots) > 2:
        sorted_snapshots = sort_snapshots_by_date(snapshots)
        delete_old_snapshots(sorted_snapshots)

if __name__ == "__main__":
    cleanup_snapshots()
