import {
  FaHome,
  FaProjectDiagram,
  FaTasks,
  FaUsers,
  FaSignOutAlt,
} from "react-icons/fa";

import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

const Sidebar = () => {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="w-64 min-h-screen bg-slate-900 text-white p-5">
      <h2 className="text-2xl font-bold mb-10">Dashboard</h2>

      <ul className="space-y-6">
        <li className="flex items-center gap-3 hover:text-indigo-400 cursor-pointer">
          <FaHome /> Dashboard
        </li>

        <li className="flex items-center gap-3 hover:text-indigo-400 cursor-pointer">
          <FaProjectDiagram /> Projects
        </li>

        <li className="flex items-center gap-3 hover:text-indigo-400 cursor-pointer">
          <FaTasks /> Tasks
        </li>

        <li className="flex items-center gap-3 hover:text-indigo-400 cursor-pointer">
          <FaUsers /> Members
        </li>

        <li
          onClick={handleLogout}
          className="flex items-center gap-3 hover:text-red-400 cursor-pointer"
        >
          <FaSignOutAlt /> Logout
        </li>
      </ul>
    </div>
  );
};

export default Sidebar;