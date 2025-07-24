from google.cloud import dlp_v2

def list_inspect_templates(project_id: str):
    client = dlp_v2.DlpServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.list_inspect_templates(request={"parent": parent})
    for template in response:
        print(f"Template name: {template.name}")
        print(f"Display name: {template.display_name}")
        print(f"Create time: {template.create_time}")
        print("-" * 40)

if __name__ == "__main__":
    list_inspect_templates("infra-voyage-466111-u7")