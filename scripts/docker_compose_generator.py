import yaml
import sys

DOCKER_COMPOSE_TEMPLATE = {
    'selenium_grid': {
        'version': "3.3",
        'networks': {
            'selenium_network': {
                'driver': 'bridge'
            }
        },
        'services': {
            'selenium-hub': {
                'image': 'selenium/standalone-hub:4.10.0',
                'container_name': 'selenium-hub',
                'networks': ['selenium_network'],
                'ports': ['4444:4444']
            },
            'chrome': {
                'image': 'selenium/node-chrome:4.10.0',
                'container_name': 'chrome-node',
                'depends_on': ['selenium-hub'],
                'environment': [
                    'SE_EVENT_BUS_HOST=selenium-hub',
                    'SE_EVENT_BUS_PUBLISH_PORT=4442',
                    'SE_EVENT_BUS_SUBSCRIBE_PORT=4443'
                ],
                'networks': ['selenium_network']
            },
            'firefox': {
                'image': 'selenium/node-firefox:4.10.0',
                'container_name': 'firefox-node',
                'depends_on': ['selenium-hub'],
                'environment': [
                    'SE_EVENT_BUS_HOST=selenium-hub',
                    'SE_EVENT_BUS_PUBLISH_PORT=4442',
                    'SE_EVENT_BUS_SUBSCRIBE_PORT=4443'
                ],
                'networks': ['selenium_network']
            },
            'nginx': {
                'image': 'nginx:alpine',
                'container_name': 'nginx-server',
                'ports': ['8081:80'],
                'volumes': ['./nginx/html:/usr/share/nginx/html'],
                'networks': ['selenium_network']
            }
        }
    }
}

def generate_docker_compose(project_type, mode, num_firefox_nodes, num_chrome_nodes, num_chromium_nodes, num_edge_nodes):
    if project_type in DOCKER_COMPOSE_TEMPLATE:
        docker_compose = DOCKER_COMPOSE_TEMPLATE[project_type]
        
        if mode == 'node':
            for i in range(num_firefox_nodes):
                docker_compose['services'][f'firefox-node-{i+1}'] = {
                    'image': 'selenium/node-firefox:4.10.0',
                    'container_name': f'firefox-node-{i+1}',
                    'depends_on': ['selenium-hub'],
                    'environment': [
                        'SE_EVENT_BUS_HOST=selenium-hub',
                        'SE_EVENT_BUS_PUBLISH_PORT=4442',
                        'SE_EVENT_BUS_SUBSCRIBE_PORT=4443'
                    ],
                    'networks': ['selenium_network']
                }


        with open('docker-compose.yml', 'w') as f:
            yaml.dump(docker_compose, f)
        print("✅ Docker Compose file generated successfully.")
    else:
        print(f"Error: Project type '{project_type}' is not recognized.")
        sys.exit(1)
