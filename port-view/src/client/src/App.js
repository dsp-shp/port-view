// import logo from './logo.svg';
// import './App.css';
// App.js
import React, { useState, useEffect } from "react";

function App() {
  const [emps, setEmps] = useState([]);
  const [search, setSearch] = useState("");
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:4567/emps", {
      method: "GET",
      headers: {
        Accept: "application/json; charset=utf-8",
      },
    })
      .then((res) => res.json())
      .then((data) => setEmps(data));
  }, []);

  console.log(emps);

  const filteredEmps = emps.filter((emp) =>
    `${emp.first_name} ${emp.last_name}`
      .toLowerCase()
      .includes(search.toLowerCase()),
  );

  return (
    <div style={{ display: "flex", height: "100vh", fontFamily: "sans-serif" }}>
      {/* Левая панель */}
      <div
        style={{
          flex: 1,
          borderRight: "1px solid #ddd",
          display: "flex",
          flexDirection: "column",
          padding: 20,
        }}
      >
        <input
          type="text"
          placeholder="Поиск сотрудника..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{
            marginBottom: 12,
            padding: 8,
            fontSize: 16,
            borderRadius: 4,
            border: "1px solid #ccc",
          }}
        />
        <div style={{ flex: 1, overflowY: "auto" }}>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr style={{ background: "#f7f7f7" }}>
                <th style={{ textAlign: "left", padding: 8 }}>Имя</th>
                <th style={{ textAlign: "left", padding: 8 }}>Должность</th>
                <th style={{ textAlign: "left", padding: 8 }}>Отдел</th>
              </tr>
            </thead>
            <tbody>
              {filteredEmps.map((emp) => (
                <tr
                  key={emp.id}
                  style={{
                    cursor: "pointer",
                    background: selected?.id === emp.id ? "#eef" : undefined,
                  }}
                  onClick={() => setSelected(emp)}
                >
                  <td style={{ padding: 8 }}>
                    {emp.first_name} {emp.last_name}
                  </td>
                  <td style={{ padding: 8 }}>{emp.position}</td>
                  <td style={{ padding: 8 }}>{emp.department}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Правая панель */}
      <div style={{ flex: 1, padding: 20 }}>
        {selected ? (
          <div
            style={{
              maxWidth: 420,
              background: "#fcfcfc",
              borderRadius: 8,
              boxShadow: "0 0 8px #eee",
              padding: 24,
            }}
          >
            <h2 style={{ marginBottom: 0 }}>
              {selected.first_name} {selected.last_name}
            </h2>
            <p style={{ margin: "12px 0 0 0", color: "#888" }}>
              {selected.position}, {selected.department}
            </p>
            <hr style={{ margin: "18px 0" }} />
            <div>
              <b>ID:</b> {selected.id}
              <br />
              <b>Возраст:</b> {selected.age}
              <br />
              <b>Email:</b> {selected.email}
              <br />
              <b>Телефон:</b> {selected.phone}
              <br />
              <b>Дата поступления:</b> {selected.hire_date}
              <br />
              <b>Зарплата:</b> {selected.salary} ₽<br />
              <b>Активен:</b> {selected.is_active ? "Да" : "Нет"}
              <br />
            </div>
          </div>
        ) : (
          <span style={{ color: "#bbb" }}>
            Выберите сотрудника из таблицы слева
          </span>
        )}
      </div>
    </div>
  );
}

export default App;

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

// export default App;
