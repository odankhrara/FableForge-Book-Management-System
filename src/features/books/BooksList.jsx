import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchBooks, deleteBook } from "./booksSlice";

export default function BooksList(){
  const dispatch = useDispatch();
  const { items, loading, error } = useSelector(s=>s.books);

  useEffect(()=>{ dispatch(fetchBooks()); },[dispatch]);  // ← auto fetch

  if(loading) return <p>Loading…</p>;
  if(error)   return <p style={{color:"red"}}>{String(error)}</p>;

  return (
    <>
      <h2>All Books</h2>
      {items.length===0 ? <p>No books yet.</p> : (
        <table className="books-table">
          <thead><tr><th>ID</th><th>Title</th><th>Author ID</th><th>ISBN</th><th>Copies</th><th>Actions</th></tr></thead>
          <tbody>
            {items.map(b=>(
              <tr key={b.id}>
                <td>{b.id}</td><td>{b.title}</td><td>{b.author_id}</td><td>{b.isbn}</td><td>{b.available_copies}</td>
                <td><button className="btn btn-delete" onClick={()=>dispatch(deleteBook(b.id))}>Delete</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </>
  );
}
