import argparse
import sys
from scripts.config_generator import generate_config, generate_valid_files
from scripts.docker_compose_generator import generate_docker_compose

def main():
    parser = argparse.ArgumentParser(description="Generate project configurations.")
    parser.add_argument("--project_type", required=True, choices=['laravel', 'django', 'php', 'python', 'nginx'], help="Project type (laravel, django, php, python or nginx).")
    parser.add_argument("--mode", required=True, choices=['standalone', 'node'], help="Choose 'standalone' or 'node' mode.")
    parser.add_argument("--num_firefox_nodes", type=int, default=0, help="Number of Firefox nodes (for node mode).")
    parser.add_argument("--num_chrome_nodes", type=int, default=0, help="Number of Chrome nodes (for node mode).")
    parser.add_argument("--num_chromium_nodes", type=int, default=0, help="Number of Chromium nodes (for node mode).")
    parser.add_argument("--num_edge_nodes", type=int, default=0, help="Number of Edge nodes (for node mode).")
    
    parser.add_argument("--test_num", type=int, default=5, help="Number of tests")
    parser.add_argument("--solution", type=str, default="solution.py", help="Solution file")

    args = parser.parse_args()

    solution_file = args.solution
    generate_config(solution_file, args.project_type, args.test_num)
    generate_valid_files(solution_file)

    generate_docker_compose(args.project_type, args.mode, args.num_firefox_nodes, args.num_chrome_nodes, args.num_chromium_nodes, args.num_edge_nodes)

if __name__ == "__main__":
    main()
