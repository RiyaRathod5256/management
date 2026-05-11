const TaskCard = () => {
  return (
    <div className="bg-white p-5 rounded-xl shadow-md">
      <h2 className="text-xl font-bold mb-2">Task Title</h2>

      <p className="text-gray-600 mb-4">
        Complete frontend integration with backend API.
      </p>

      <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm">
        Pending
      </span>
    </div>
  );
};

export default TaskCard;