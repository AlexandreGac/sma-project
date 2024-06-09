use std::fs::File;
use std::io::{self, prelude::*, BufReader};
use std::str::FromStr;

fn main() -> io::Result<()> {
    let file = File::open("src/Emissions.xml")?;
    let reader = BufReader::new(file);

    let mut count = 0;
    let mut total_duration = 0.0;
    let mut duration_count = 0.0;
    for line in reader.lines() {
        count += 1;
        println!("{count}");
        let Ok(content) = line else { panic!() };
        let content: Vec<char> = content.chars().collect();
        for i in 0..content.len() {
            if content[i] == 'C' && content[i + 1] == 'O' && content[i + 2] == '2' && content[i + 3] == '=' {
                let mut j = i + 5;
                let mut quantity = String::new();
                while content[j] != '"' {
                    quantity.push(content[j]);
                    j += 1;
                }
                let number = f64::from_str(quantity.as_str()).expect("Ptdrrr");
                total_duration += number;
                duration_count += 1.0;
                continue;
            }
        }
    }
    let mean_duration = total_duration / duration_count;
    println!("CO2 : {total_duration}");

    Ok(())
}