function Header({ theme }) {
  return <h2 style={{ color: theme === "Light" ? "black" : "white" }}>Header - {theme} Theme</h2>;
}

export default Header;