//Bootstraping driver for downloading python interpreter
use reqwest::Client;
use std::fs;
use std::process::Command;
mod downloader;
mod unziper;

#[tokio::main]

async fn main() {
    let python_version = "3.10.5";
    let interpreter_url: String = format!(
        "https://www.python.org/ftp/python/{}/python-{}-embed-amd64.zip",
        python_version, python_version
    );
    let pip_url: &str = "https://bootstrap.pypa.io/get-pip.py";
    let tmp_file: &str = "./tmp/python";

    if !(std::path::Path::new("./Python/python.exe").exists()) || !(std::path::Path::new("./Python/Scripts/pip.exe").exists()){
        println!("Downloading Python...");
        downloader::file_from_url(&Client::new(), &interpreter_url, tmp_file)
            .await
            .unwrap();
        println!("Extracting...");
        unziper::deflate(tmp_file).await;
        match fs::create_dir("./Python/DLLs") {
            Ok(()) => {
                println!("Created DLL directory.");
            }
            Err(err) => {
                println!("DLL directory already exists: {}", err);
            }
        }
        for element in std::path::Path::new("./Python").read_dir().unwrap() {
            let pth_path = element.unwrap().path();
            if let Some(extension) = pth_path.extension() {
                if extension == "_pth" {
                    println!("Found _pth file: {}", pth_path.display());
                    let new_name = pth_path.with_extension("pth");
                    println!("Renaming to: {}", new_name.display());
                    fs::rename(pth_path, new_name).unwrap();
                }
            }
        }
        println!("Downloading pip...");
        let get_pip_path = "./Python/get-pip.py";
        downloader::file_from_url(&Client::new(), pip_url, get_pip_path)
            .await
            .unwrap();
        println!("Complete.");

        Command::new("./Python/python.exe")
            .arg("--version")
            .spawn()
            .expect("Python interpreter failed to launch...");

        Command::new("./Python/python.exe")
            .arg(get_pip_path)
            .spawn()
            .expect("Failed to get pip...");
    }

    std::env::set_current_dir("../").unwrap();

    if !(std::path::Path::new("./launcher/Python/Scripts/flask.exe").exists()) {
        println!("Launching DAQ-Tool Updater...");
        Command::new("./launcher/Python/python.exe")
            .env(
                "PATH",
                "./launcher/Python;./launcher/Python/Scripts;./launcher/Git/bin;./launcher/Git/cmd",
            )
            .arg("./daqcli.py")
            .arg("update")
            .spawn()
            .expect("Failed to run daqcli updater...");
    } else {
        println!("Launching DAQ-Tool CLI...");
        Command::new("./launcher/Python/python.exe")
            .env(
                "PATH",
                "./launcher/Python;./launcher/Python/Scripts;./launcher/Git/bin;./launcher/Git/cmd",
            )
            .arg("./daqcli.py")
            .arg("run")
            .spawn()
            .expect("Failed to run daqcli dashboard...");
    }
}
