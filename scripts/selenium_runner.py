import os
from scripts.docker_handler import DockerHandler
import docker
import subprocess
import time
import requests
from selenium import webdriver

class SeleniumRunner:
    SOLUTION_FOLDER = os.path.abspath("solution")
    TEST_CASES_FOLDER = os.path.abspath("test_cases")
    DOCKER_EXEC = ["docker-compose", "exec", "-T", "asm-container"]

    @staticmethod
    def health_selenium(cls):
        for service in ["selenium-hub", "chrome-node", "firefox-node", "nginx-server"]:
            container_list = cls.docker_client.containers.list(filters={"name": service})
            if container_list:
                cls.containers[service] = container_list[0]
                print(f"Container {service} is running.")
            else:
                print(f"Container {service} is not running!")

        subprocess.run("docker ps".split(), check=True)

        cls.chrome_driver = cls.get_webdriver("chrome")
        cls.firefox_driver = cls.get_webdriver("firefox")

    @staticmethod
    def wait_for_services_to_start(cls):
        hub_url = "http://localhost:4444/wd/hub"
        timeout = 60
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                response = requests.get(hub_url + "/status", timeout=10)
                if response.status_code == 200 and response.json()["value"]["ready"]:
                    print("Selenium Hub is ready.")
                    return
            except requests.exceptions.RequestException:
                pass
            time.sleep(2)

        print("Selenium Hub did not become ready within the timeout period.")

    @staticmethod
    def get_webdriver(cls, browser):
        print(f"Initializing WebDriver for {browser}...")
        options = webdriver.ChromeOptions() if browser == "chrome" else webdriver.FirefoxOptions()
        return webdriver.Remote(command_executor="http://localhost:4444/wd/hub", options=options)