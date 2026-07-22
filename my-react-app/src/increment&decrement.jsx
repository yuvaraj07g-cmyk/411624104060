import { useState } from "react";
  return (
    <div>
      <h1>Counter App</h1>
      <h2>{count}</h2>
      <button onClick={()=>{
        setCount(count+1);
      }}>Increment</button>

      <button onClick={()=>{
        setCount(count-1);
      }}> Decrement</button>

      <button onClick={()=>{
        setCount(0);
      }}>Reset</button>
    </div>
  );

export default App;