import DashboardLayout from "../layouts/DashboardLayout";
import TaskCard from "../components/TaskCard";

const MemberDashboard = () => {
  const tasks = [
    {
      id: 1,
      title: "Build Authentication UI",
      due_date: "2026-05-20",
      status: "Pending",
      priority: "High",
      project_name: "Task Manager",
    },
    {
      id: 2,
      title: "Connect Backend APIs",
      due_date: "2026-05-24",
      status: "In Progress",
      priority: "Medium",
      project_name: "CRM System",
    },
    {
      id: 3,
      title: "Fix Dashboard Bugs",
      due_date: "2026-05-28",
      status: "Completed",
      priority: "Low",
      project_name: "Admin Panel",
    },
  ];

  const handleStatusChange = (id, status) => {
    console.log("Task:", id);
    console.log("Status:", status);
  };

  return (
    <DashboardLayout>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800">
          Member Dashboard
        </h1>

        <p className="text-gray-500 mt-1">
          View and manage assigned tasks
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        {tasks.map((task) => (
          <TaskCard
            key={task.id}
            task={task}
            onStatusChange={handleStatusChange}
          />
        ))}
      </div>
    </DashboardLayout>
  );
};

export default MemberDashboard;