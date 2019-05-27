import React, { useState } from "react";
import logo from "./logo.svg";
import "./App.css";
import Axios from "axios";

function App() {
  const [tweet, setTweet] = useState("");
  const [result, setResult] = useState("");
  const handleSubmit = async () => {
    if (tweet === "") {
      window.alert("Konten tweet tidak boleh kosong.");
      return;
    } else if (tweet.length > 280) {
      window.alert("Konten tweet tidak boleh lebih dari 280 karakter");
      return;
    }
    console.log(tweet);
    let numOfRetry = 2;
    setResult("Loading...");
    while (numOfRetry > 0) {
      try {
        const { data, status } = await Axios.post(
          "https://id-tweet-depression-detection.herokuapp.com",
          {
            tweet: tweet
          }
        );
        console.log(data, status);
        const message = data["LinearSVC"];
        setResult(message);
        if (status === 200) {
          numOfRetry = 0;
        }
      } catch (e) {
        setResult("Oops. There is some error. Sorry!");
        console.log(e);
      }
      --numOfRetry;
    }
  };
  return (
    <div className="App">
      <header className="App-header">
        <h1>Deteksi Depresi Twitter</h1>
        <div>
          <h2>Masukkan konten Tweet anda (maksimum 280 karakter)</h2>
          <textarea
            value={tweet}
            onChange={e => setTweet(e.target.value)}
            style={{
              width: "80%",
              height: "2rem"
            }}
          />
        </div>
        <button onClick={handleSubmit}>Submit</button>
        {result && <h4>{result}</h4>}
      </header>
    </div>
  );
}

export default App;
