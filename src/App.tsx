import { useParams, HashRouter, Link, Route, Routes } from "react-router-dom";
import { ExerciseList } from "./pages/ExerciseList";
import { ExerciseView } from "./pages/ExerciseView";
import "./App.css";

/**
 * Remounts the view when the exercise changes. Without the key React reuses
 * the instance across :id changes and the previous exercise's code stays put.
 */
function ExerciseRoute() {
  const { id } = useParams();
  return <ExerciseView key={id} />;
}

function NotFound() {
  return (
    <div className="page">
      <p className="empty">
        Nothing here. <Link to="/">Back to the exercises</Link>.
      </p>
    </div>
  );
}

// Hash routing, not history routing: GitHub Pages serves static files with no
// SPA rewrite, so /code-lab/exercise/two-sum would 404 on refresh or a shared
// link. It also matches the other GraphL apps, which all route on #/<id>.
export default function App() {
  return (
    <HashRouter>
      <Routes>
        <Route path="/" element={<ExerciseList />} />
        <Route path="/exercise/:id" element={<ExerciseRoute />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </HashRouter>
  );
}
