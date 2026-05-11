import DashboardLayout from "../layouts/DashboardLayout";
import ProjectTable from "../components/ProjectTable";

const AdminDashboard = () => {
  const projects = [
    {
      id: 1,
      name: "Task Manager System",
      status: "In Progress",
      deadline: "2026-06-15",
    },
    {
      id: 2,
      name: "E-Commerce Website",
      status: "Completed",
      deadline: "2026-05-28",
    },
  ];

  return (
    <DashboardLayout>
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">
            Admin Dashboard
          </h1>

          <p className="text-gray-500 mt-1">
            Manage projects and tasks
          </p>
        </div>

        <button className="bg-indigo-600 hover:bg-indigo-700 text-white px-5 py-3 rounded-xl shadow-md">
          + Create Project
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
        <div className="bg-white p-6 rounded-2xl shadow-md">
          <p className="text-gray-500">Total Projects</p>

          <h2 className="text-3xl font-bold mt-2">
            12
          </h2>
        </div>

        <div className="bg-white p-6 rounded-2xl shadow-md">
          <p className="text-gray-500">Total Tasks</p>

          <h2 className="text-3xl font-bold mt-2">
            45
          </h2>
        </div>

        <div className="bg-white p-6 rounded-2xl shadow-md">
          <p className="text-gray-500">In Progress</p>

          <h2 className="text-3xl font-bold mt-2 text-yellow-500">
            9
          </h2>
        </div>

        <div className="bg-white p-6 rounded-2xl shadow-md">
          <p className="text-gray-500">Completed</p>

          <h2 className="text-3xl font-bold mt-2 text-green-500">
            36
          </h2>
        </div>
      </div>

      <ProjectTable projects={projects} />

      <div className="grid lg:grid-cols-2 gap-8 mt-10">
        <div className="bg-white p-6 rounded-2xl shadow-md">
          <h2 className="text-2xl font-bold mb-5">
            Recent Tasks
          </h2>

          <div className="space-y-4">
            <div className="border p-4 rounded-xl">
              <h3 className="font-semibold">
                Build Login API
              </h3>

              <p className="text-gray-500 text-sm">
                Assigned to Rahul
              </p>
            </div>

            <div className="border p-4 rounded-xl">
              <h3 className="font-semibold">
                Design Dashboard UI
              </h3>

              <p className="text-gray-500 text-sm">
                Assigned to Aman
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl shadow-md">
          <h2 className="text-2xl font-bold mb-5">
            Assign Task
          </h2>

          <form className="space-y-4">
            <input
              type="text"
              placeholder="Task title"
              className="w-full border p-3 rounded-xl"
            />

            <input
              type="text"
              placeholder="Assign member"
              className="w-full border p-3 rounded-xl"
            />

            <input
              type="date"
              className="w-full border p-3 rounded-xl"
            />

            <button className="w-full bg-indigo-600 hover:bg-indigo-700 text-white py-3 rounded-xl">
              Create Task
            </button>
          </form>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default AdminDashboard;