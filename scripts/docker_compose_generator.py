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
            'edge': {
                'image': 'selenium/node-edge:4.10.0',
                'container_name': 'edge-node',
                'depends_on': ['selenium-hub'],
                'environment': [
                    'SE_EVENT_BUS_HOST=selenium-hub',
                    'SE_EVENT_BUS_PUBLISH_PORT=4442',
                    'SE_EVENT_BUS_SUBSCRIBE_PORT=4443'
                ],
                'networks': ['selenium_network']
            },
            'chromium': {
                'image': 'selenium/node-chromium:4.10.0',
                'container_name': 'chromium-node',
                'depends_on': ['selenium-hub'],
                'environment': [
                    'SE_EVENT_BUS_HOST=selenium-hub',
                    'SE_EVENT_BUS_PUBLISH_PORT=4442',
                    'SE_EVENT_BUS_SUBSCRIBE_PORT=4443'
                ],
                'networks': ['selenium_network']
            },
            'nginx': {
                'image': 'nginx:1.20.2-alpine',
                'container_name': 'nginx-server',
                'ports': ['8081:80'],
                'volumes': ['./nginx/html:/usr/share/nginx/html'],
                'networks': ['selenium_network']
            }
        }
    },
    'standalone': {
        'version': "3.3",
        'networks': {
            'selenium_network': {
                'driver': 'bridge'
            }
        },
        'services': {
            'chrome': {
                'image': 'selenium/standalone-chrome:4.10.0',
                'container_name': 'chrome-standalone',
                'ports': ['4444:4444'],
                'networks': ['selenium_network']
            },
            'firefox': {
                'image': 'selenium/standalone-firefox:4.10.0',
                'container_name': 'firefox-standalone',
                'ports': ['4444:4444'],
                'networks': ['selenium_network']
            },
            'chromium': {
                'image': 'selenium/standalone-chromium:4.10.0',
                'container_name': 'chromium-standalone',
                'ports': ['4444:4444'],
                'networks': ['selenium_network']
            },
            'edge': {
                'image': 'selenium/standalone-edge:4.10.0',
                'container_name': 'edge-standalone',
                'ports': ['4444:4444'],
                'networks': ['selenium_network']
            },
            'nginx': {
                'image': 'nginx:1.20.2-alpine',
                'container_name': 'nginx-server',
                'ports': ['8081:80'],
                'volumes': ['./nginx/html:/usr/share/nginx/html'],
                'networks': ['selenium_network']
            }
        },
        'networks': {
            'selenium_network': {
                'driver': 'bridge'
            }
        }
    },
    'php': {
        'version': "3.3",
        'networks': {
            'selenium_network': {
                'driver': 'bridge'
            }
        },
        'services': {
            'php': {
                'image': 'php:7.4-apache',
                'container_name': 'php-container',
                'ports': ['80:80'],
                'volumes': ['./php:/var/www/html'],
                'networks': ['default']
            }
        }
    },
    'laravel': {
        'version': "3.3",
        'networks': {
            'selenium_network': {
                'driver': 'bridge'
            }
        },
        'services': {
            'php': {
                'image': 'php:7.4-fpm',
                'container_name': 'laravel-php',
                'ports': ['9000:9000'],
                'volumes': ['./laravel:/var/www/html'],
                'networks': ['default']
            },
            'nginx': {
                'image': 'nginx:1.20.2-alpine',
                'container_name': 'nginx',
                'ports': ['80:80'],
                'volumes': ['./nginx:/etc/nginx/sites-enabled'],
                'networks': ['default']
            }
        }
    },
    'django': {
        'version': "3.3",
        'networks': {
            'selenium_network': {
                'driver': 'bridge'
            }
        },
        'services': {
            'python': {
                'image': 'python:3.9',
                'container_name': 'django-container',
                'volumes': ['./django:/app'],
                'working_dir': '/app',
                'command': 'python manage.py runserver 0.0.0.0:8000',
                'ports': ['8000:8000'],
                'networks': ['default']
            },
            'nginx': {
                'image': 'nginx:1.20.2-alpine',
                'container_name': 'nginx',
                'ports': ['80:80'],
                'volumes': ['./nginx:/etc/nginx/sites-enabled'],
                'networks': ['default']
            }
        }
    },
    'flask': {
        'version': "3.3",
        'networks': {
            'selenium_network': {
                'driver': 'bridge'
            }
        },
        'services': {
            'flask': {
                'image': 'python:3.9',
                'container_name': 'flask-container',
                'volumes': ['./flask:/app'],
                'working_dir': '/app',
                'command': 'python app.py',
                'ports': ['5000:5000'],
                'networks': ['default']
            },
            'nginx': {
                'image': 'nginx:1.20.2-alpine',
                'container_name': 'nginx',
                'ports': ['80:80'],
                'volumes': ['./nginx:/etc/nginx/sites-enabled'],
                'networks': ['default']
            }
        }
    },
    'python': {
        'version': "3.3",
        'networks': {
            'selenium_network': {
                'driver': 'bridge'
            }
        },
        'services': {
            'python': {
                'image': 'python:3.9',
                'container_name': 'python-container',
                'volumes': ['./python:/app'],
                'working_dir': '/app',
                'command': 'python app.py',
                'ports': ['5000:5000'],
                'networks': ['default']
            }
        }
    },
    'nginx': {
        'version': "3.3",
        'networks': {
            'selenium_network': {
                'driver': 'bridge'
            }
        },
        'services': {
            'nginx': {
                'image': 'nginx:1.20.2-alpine',
                'container_name': 'nginx',
                'ports': ['8081:80'],
                'volumes': ['./nginx:/usr/share/nginx/html'],
                'networks': ['default']
            }
        }
    }
}

def generate_docker_compose(project_type, mode, num_firefox_nodes, num_chrome_nodes, num_chromium_nodes, num_edge_nodes):
    if project_type in DOCKER_COMPOSE_TEMPLATE:
        docker_compose = DOCKER_COMPOSE_TEMPLATE[project_type]
        
        if mode == 'node':
            
            docker_compose['services']['selenium-hub'] = {
                    'image': 'selenium/hub:4.10.0',
                    'container_name': 'selenium-hub',
                    'ports': ['4444:4444'],
                    'networks': ['selenium_network']
                }
            
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

            for i in range(num_chrome_nodes):
                docker_compose['services'][f'chrome-node-{i+1}'] = {
                    'image': 'selenium/node-chrome:4.10.0',
                    'container_name': f'chrome-node-{i+1}',
                    'depends_on': ['selenium-hub'],
                    'environment': [
                        'SE_EVENT_BUS_HOST=selenium-hub',
                        'SE_EVENT_BUS_PUBLISH_PORT=4442',
                        'SE_EVENT_BUS_SUBSCRIBE_PORT=4443'
                    ],
                    'networks': ['selenium_network']
                }

            for i in range(num_chromium_nodes):
                docker_compose['services'][f'chromium-node-{i+1}'] = {
                    'image': 'selenium/node-chromium:4.10.0',
                    'container_name': f'chromium-node-{i+1}',
                    'depends_on': ['selenium-hub'],
                    'environment': [
                        'SE_EVENT_BUS_HOST=selenium-hub',
                        'SE_EVENT_BUS_PUBLISH_PORT=4442',
                        'SE_EVENT_BUS_SUBSCRIBE_PORT=4443'
                    ],
                    'networks': ['selenium_network']
                }

            for i in range(num_edge_nodes):
                docker_compose['services'][f'edge-node-{i+1}'] = {
                    'image': 'selenium/node-edge:4.10.0',
                    'container_name': f'edge-node-{i+1}',
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
