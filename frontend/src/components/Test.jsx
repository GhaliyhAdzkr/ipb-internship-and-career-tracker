import { useState } from "react";
// Assuming your JSON is in the same directory
import data from "../data/items.json"; 

function Test() {
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 6;

  // 1. Calculate Pagination Indices
  const lastIndex = currentPage * itemsPerPage;
  const firstIndex = lastIndex - itemsPerPage;
  
  // 2. Slice the JSON array
  const currentCards = data.slice(firstIndex, lastIndex);
  const totalPages = Math.ceil(data.length / itemsPerPage);

  return (
    <div className="flex flex-col min-h-screen p-6">
      {/* 3. The Grid Layout */}
      <div className="flex-1 grid grid-cols-2 xl:grid-cols-3 gap-6 content-start">
        {currentCards.map((item) => (
          <div key={item._id} className="group p-5 bg-white border border-gray-200 rounded-xl hover:shadow-lg transition-all">
            <div className="h-40 bg-gray-100 rounded-lg mb-4 overflow-hidden">
                <img src={item.imageUrl} alt={item.title} className="w-full h-full object-cover group-hover:scale-110 transition-transform" />
            </div>
            <h3 className="font-bold text-lg group-hover:text-blue-600">{item.title}</h3>
            <p className="text-gray-500 line-clamp-2">{item.name}</p>
          </div>
        ))}
      </div>

      {/* 4. Pagination Controls */}
      <div className="mt-10 flex justify-center gap-4">
        <button 
          disabled={currentPage === 1}
          onClick={() => setCurrentPage(prev => prev - 1)}
          className="px-4 py-2 bg-white border rounded-md disabled:opacity-30 hover:bg-gray-50"
        >
          Previous
        </button>

        <div className="flex items-center gap-2">
           {Array.from({ length: totalPages }, (_, i) => (
             <button
               key={i + 1}
               onClick={() => setCurrentPage(i + 1)}
               className={`w-8 h-8 rounded ${currentPage === i + 1 ? 'bg-blue-600 text-white' : 'hover:bg-gray-100'}`}
             >
               {i + 1}
             </button>
           ))}
        </div>

        <button 
          disabled={currentPage === totalPages}
          onClick={() => setCurrentPage(prev => prev + 1)}
          className="px-4 py-2 bg-white border rounded-md disabled:opacity-30 hover:bg-gray-50"
        >
          Next
        </button>
      </div>
    </div>
  );
}
export default Test;