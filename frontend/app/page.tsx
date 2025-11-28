"use client";
import { useState } from "react";

export default function Home() {
  const [token, setToken] = useState<string | null>(null);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [text, setText] = useState("");
  const [direction, setDirection] = useState("fr-en");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const auth = async (endpoint: string) => {
    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);

    // Pour /register, l'API attend du JSON, pour /login du Form data (OAuth2 standard)
    const isLogin = endpoint === "login";
    const headers = isLogin 
      ? { "Content-Type": "application/x-www-form-urlencoded" }
      : { "Content-Type": "application/json" };
    
    const body = isLogin ? formData : JSON.stringify({ username, password });

    try {
      const res = await fetch(`http://127.0.0.1:8000/${endpoint}`, { 
        method: "POST", headers, body 
      });
      const data = await res.json();
      if (res.ok && isLogin) setToken(data.access_token);
      else alert(JSON.stringify(data));
    } catch (e) { alert("Erreur réseau"); }
  };

  const translate = async () => {
    setLoading(true);
    setResult("");
    try {
      const res = await fetch("http://127.0.0.1:8000/translate", {
        method: "POST",
        headers: { 
          "Content-Type": "application/json", 
          "Authorization": `Bearer ${token}` 
        },
        body: JSON.stringify({ text, direction }),
      });
      const data = await res.json();
      if (res.ok) setResult(data.translation);
      else alert(data.detail);
    } catch (e) { alert("Erreur traduction"); }
    setLoading(false);
  };

  if (!token) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
        <h1 className="text-2xl font-bold mb-4">TalAIt Authentification </h1>
        <div className="bg-white p-6 rounded shadow-md w-80">
          <input className="border p-2 w-full mb-2" placeholder="Username" onChange={e => setUsername(e.target.value)} />
          <input className="border p-2 w-full mb-4" type="password" placeholder="Password" onChange={e => setPassword(e.target.value)} />
          <div className="flex gap-2">
            <button onClick={() => auth("login")} className="bg-blue-500 text-white p-2 w-full rounded">Login</button>
            <button onClick={() => auth("register")} className="bg-green-500 text-white p-2 w-full rounded">Register</button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-2xl mx-auto bg-white p-6 rounded shadow">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold text-blue-600">TalAIt Traduction</h1>
          <button onClick={() => setToken(null)} className="text-red-500 text-sm">Logout</button>
        </div>
        
        <textarea 
          className="w-full border p-3 rounded h-32 mb-4" 
          placeholder="Texte à traduire..." 
          value={text} 
          onChange={e => setText(e.target.value)} 
        />
        
        <div className="flex gap-4 mb-4">
          <select 
            className="border p-2 rounded flex-1" 
            value={direction} 
            onChange={e => setDirection(e.target.value)}>
            <option value="fr-en">Français ➡️ Anglais</option>
            <option value="en-fr">Anglais ➡️ Français</option>
          </select>
          <button 
            onClick={translate} 
            disabled={loading}
            className="bg-blue-600 text-white px-6 py-2 rounded font-bold disabled:bg-gray-400">
            {loading ? "..." : "Traduire"}
          </button>
        </div>

        {result && (
          <div className="bg-green-50 border border-green-200 p-4 rounded text-green-900">
            <strong>Résultat :</strong> {result}
          </div>
        )}
      </div>
    </div>
  );
} 