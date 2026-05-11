const ProjectTable = () => {
  return (
    <div className="bg-white p-5 rounded-xl shadow-md">
      <h2 className="text-2xl font-bold mb-4">Projects</h2>

      <table className="w-full border-collapse">
        <thead>
          <tr className="bg-gray-100">
            <th className="p-3 text-left">Project</th>
            <th className="p-3 text-left">Status</th>
            <th className="p-3 text-left">Deadline</th>
          </tr>
        </thead>

        <tbody>
          <tr className="border-b">
            <td className="p-3">Task Manager</td>
            <td className="p-3">In Progress</td>
            <td className="p-3">15 May 2026</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default ProjectTable;