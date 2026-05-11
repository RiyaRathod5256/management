import Navbar from "../components/Navbar";
import { motion } from "framer-motion";
import { Link } from "react-router-dom";

const Home = () => {
  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar />

      <section className="flex flex-col justify-center items-center text-center px-6 py-24">
        <motion.h1
          initial={{ opacity: 0, y: -40 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-5xl font-bold text-gray-800 mb-6"
        >
          Task Management System
        </motion.h1>

        <p className="text-gray-600 max-w-2xl mb-8 text-lg">
          Manage projects, assign tasks, track progress,
          and improve team productivity.
        </p>

        <Link
          to="/register"
          className="bg-indigo-600 hover:bg-indigo-700 text-white px-8 py-4 rounded-2xl shadow-lg"
        >
          Get Started
        </Link>
      </section>

      <section className="grid md:grid-cols-3 gap-6 px-10 pb-20">
        <div className="bg-white p-6 rounded-2xl shadow-md">
          <h2 className="text-2xl font-bold mb-3">
            Project Management
          </h2>

          <p className="text-gray-600">
            Organize and manage projects easily.
          </p>
        </div>

        <div className="bg-white p-6 rounded-2xl shadow-md">
          <h2 className="text-2xl font-bold mb-3">
            Team Collaboration
          </h2>

          <p className="text-gray-600">
            Assign tasks and collaborate with members.
          </p>
        </div>

        <div className="bg-white p-6 rounded-2xl shadow-md">
          <h2 className="text-2xl font-bold mb-3">
            Analytics
          </h2>

          <p className="text-gray-600">
            Track progress with dashboard analytics.
          </p>
        </div>
      </section>
    </div>
  );
};

export default Home;