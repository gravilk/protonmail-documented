use rocket::{get, post, routes};
use rocket::serde::json::{Json, Value};
use rocket::launch;
use sha2::{Digest, Sha256};

const N_LEADING_ZEROS_REQUIRED: usize = 13;

#[derive(serde::Deserialize)]
struct ChallengeRequest {
    challenges: Vec<String>,
}

#[derive(serde::Serialize)]
struct SolutionResponse {
    solutions: Vec<u64>,
}

fn solve_challenge(challenge: &str) -> u64 {
    let mut curr = 0;
    loop {
        let input = format!("{}{}", curr, challenge);
        let result = Sha256::digest(input.as_bytes());
        let hex_string = format!("{:x}", result);

        let j = (N_LEADING_ZEROS_REQUIRED + 3) / 4;
        let k = &hex_string[..j];
        let l = u64::from_str_radix(k, 16).unwrap();

        if l < 2u64.pow(4 * j as u32 - N_LEADING_ZEROS_REQUIRED as u32) {
            return curr;
        } else {
            curr += 1;
        }
    }
}

#[post("/solve", format = "json", data = "<request>")]
fn solve_challenges(request: Json<ChallengeRequest>) -> Json<SolutionResponse> {
    let solutions: Vec<u64> = request
        .challenges
        .iter()
        .map(|challenge| solve_challenge(challenge))
        .collect();

    Json(SolutionResponse { solutions })
}

#[get("/")]
fn index() -> &'static str {
    "Welcome to the challenge solver API!"
}

#[launch]
fn rocket() -> _ {
    rocket::build().mount("/", routes![index, solve_challenges])
}