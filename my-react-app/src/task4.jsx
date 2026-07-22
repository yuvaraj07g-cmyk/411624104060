import { useState } from "react";
import Header from "./Header";
import ThemePanel from "./ThemePanel";
import Content from "./Content";
import Footer from "./Footer";


function App() {
  const [theme, setTheme] = useState("Light");

  function toggleTheme (){
    setTheme(theme === "Light" ? "Dark" : "Light");
  };

  return (
    <div style={{color: theme === "Light" ? "black" : "white", backgroundColor: theme === "Light" ? "blue" : "black", minHeight: "100vh", padding: "20px"}}>
      <Header theme={theme} />
      <ThemePanel theme={theme} toggleTheme={toggleTheme} /> 
      <Content theme={theme} />
      <Footer theme={theme} />
    </div>
  );
}

export default App;