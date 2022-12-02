//Bootstraping driver for downloading python interpreter
use reqwest::Client;
use std::process::Command;
use std::fs;
use std::path::PathBuf;
mod downloader;
mod unziper;

#[tokio::main]

async fn main() {
    let python_version = "3.11.0";
    let url: String = format!(
        "https://www.python.org/ftp/python/{}/python-{}-embed-amd64.zip",
        python_version, python_version
    );
    let path: &str = "./tmp/python";
    println!("Downloading...");
    downloader::file_from_url(&Client::new(), &url, path)
        .await
        .unwrap();
    println!("Extracting...");
    unziper::deflate(path).await;
    println!("Complete.");
    println!("Launching DAQ-Tool CLI...");
    Command::new("./Python/python.exe")
        .arg("--version")
        .spawn()
        .expect("Python interpreter failed to launch...");

    let daqcli_rel = PathBuf::from("../daqcli.py");
    //let daqcli_abs = fs::canonicalize(daqcli_rel).unwrap();

    Command::new("./Python/python.exe")
        .spawn()
        .expect("Python interpreter failed to launch...");
}
