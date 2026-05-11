import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="bg-white shadow-md px-8 py-4 flex justify-between items-center">
      <h1 className="text-2xl font-bold text-indigo-600">
        Task Manager
      </h1>

      <div className="flex gap-4">
        <Link
          to="/login"
          className="text-gray-700 hover:text-indigo-600"
        >
          Login
        </Link>

        <Link
          to="/register"
          className="bg-indigo-600 hover:bg-indigo-700 text-white px-5 py-2 rounded-xl"
        >
          Register
        </Link>
      </div>
    </nav>
  );
};

export default Navbar;