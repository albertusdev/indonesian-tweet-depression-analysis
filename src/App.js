import React, { useState } from "react";
import logo from "./logo.svg";
import "./App.css";
import Axios from "axios";

function App() {
  const [tweet, setTweet] = useState("");
  const handleSubmit = async () => {
    if (tweet === "") {
      window.alert("Konten tweet tidak boleh kosong.");
      return;
    } else if (tweet.length > 280) {
      window.alert("Konten tweet tidak boleh lebih dari 280 karakter");
      return;
    }
    console.log(tweet);
    const { data } = Axios.post(
      "https://id-tweet-depression-detection.herokuapp.com",
      {
        tweet: tweet
      },
      {
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods":
            "GET, POST, PATCH, PUT, DELETE, OPTIONS",
          "Access-Control-Allow-Headers": "Origin, Content-Type, X-Auth-Token"
        }
      }
    );
    console.log(data);
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
      </header>
    </div>
  );
}

export default App;
