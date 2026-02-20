import { Routes, Route } from "react-router-dom";
import Home from "./pages/home";
import Auth from "./pages/auth";
import Chat from "./pages/chat";
import ProtectedRoute from "./protectedRoute";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/auth" element={<Auth />} />
      <Route path="/signup" element={<Auth />} />
      <Route path="/chat" element={
        <ProtectedRoute>
          <Chat />
        </ProtectedRoute>
      }/>
    </Routes>
  );
}

export default App;

