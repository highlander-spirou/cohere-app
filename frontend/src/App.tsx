import React, { useEffect, useState } from "react";
import { Button, Textarea } from "@/components";

const App = () => {
  const [data, setData] = useState();
  const [userInput, setUserInput] = useState("");

  const requestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ content: userInput }),
  };


  const handleChange = (event: any) => {
    setUserInput(event.target.value);
  };

  const submission = () => {
    if (!!userInput) {
      fetch("http://localhost:8000/query", requestOptions)
        .then((response) => response.json())
        .then((returnedData) => {
          setData(returnedData.res.texts);
        });
    }
  };

  return (
    <>
      <div className="text-center font-bold text-5xl">App</div>
      {!!data ? <p>Có data</p> : <p>Ko có data</p>}
      {!!data && (
        <>
          {Object.values(data).map((x, index) => {
            return <p key={index}>{x}</p>;
          })}
        </>
      )}
      <div className="flex flex-col items-center gap-3 w-full mt-20">
        <Textarea
          placeholder="Enter text"
          className="w-[650px]"
          value={userInput}
          onChange={handleChange}
        ></Textarea>
        <Button onClick={submission}>Submit</Button>
      </div>
    </>
  );
};

export default App;
