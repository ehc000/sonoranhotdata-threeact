
const API_BASE = "http://localhost:8000/api";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}

export const api = {
  getStudents: () => request("/students"),

  getStudent: (id) => request(`/students/${id}`),

  createStudent: (data) =>
    request("/students", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  getProfile: (id) => request(`/students/${id}/profile`),

  addTeacherNote: (id, section, note_text) =>
    request(`/students/${id}/notes`, {
      method: "POST",
      body: JSON.stringify({ section, note_text }),
    }),

  updatePreferences: (id, changes) =>
    request(`/students/${id}/preferences`, {
      method: "PATCH",
      body: JSON.stringify(changes),
    }),

  getProjects: (id) => request(`/students/${id}/projects`),
};
