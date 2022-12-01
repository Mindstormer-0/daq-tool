use flate2::read::GzDecoder;
use tar::Archive;
use std::fs::File;
pub async fn deflate(input_path: &str, output_path: &str) {
    let tar = File::open(input_path).unwrap();
    let dec = GzDecoder::new(tar);
    let mut a = Archive::new(dec);
    a.unpack(output_path).unwrap();
}
