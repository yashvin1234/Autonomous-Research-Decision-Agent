import type { FullAgentResponse } from "../types/agent";

const API_BASE = "http://127.0.0.1:5050";
let isLoggingOut = false;


function logout() {
  if (isLoggingOut) return;
  isLoggingOut = true;
  localStorage.removeItem("token");
  window.location.href = "/auth";
}

export async function runAgent(goal: string, chatId?: number): Promise<FullAgentResponse> {

  const token = localStorage.getItem("token");

  const response = await fetch(`${API_BASE}/chat/analyze`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({
      goal: goal,
      chat_id: chatId
    }),
  });

  if (response.status === 401) {
    logout();
    throw new Error("Session expired");
  }

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || "Agent failed");
  }
  return await response.json();
}

export async function loadRepo(repoUrl: string) {
  const token = localStorage.getItem("token");

  const res = await fetch(`${API_BASE}/repos/index`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ repo_url: repoUrl }),
  });
  
  if (res.status === 401) {
    logout();
    throw new Error("Session expired");
  }
  if (!res.ok) throw new Error("Repo load failed");
  return await res.json();
}

export async function askRepo(repoId: number, question: string) {
  const token = localStorage.getItem("token");

  const res = await fetch(`${API_BASE}/repos/ask`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ repo_id: repoId, question }),
  });

  if (res.status === 401) {
    logout();
    throw new Error("Session expired");
  }

  if (!res.ok) throw new Error("Repo query failed");
  return await res.json();
}
