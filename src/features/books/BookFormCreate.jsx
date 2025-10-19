import { useState } from "react";
import { useDispatch } from "react-redux";
import { createBook } from "./booksSlice";

export default function BookFormCreate(){
  const [f,setF]=useState({title:"",isbn:"",publication_year:"",available_copies:1,author_id:""});
  const d=useDispatch();
  const submit=e=>{
    e.preventDefault();
    d(createBook({
      title:f.title, isbn:f.isbn,
      publication_year: f.publication_year?Number(f.publication_year):null,
      available_copies: Number(f.available_copies),
      author_id: Number(f.author_id)
    })).unwrap().then(()=>setF({title:"",isbn:"",publication_year:"",available_copies:1,author_id:""}));
  };
  return (
    <form onSubmit={submit}>
      <h3>Create Book</h3>
      <input placeholder="Title" value={f.title} onChange={e=>setF({...f,title:e.target.value})} required/>
      <input placeholder="ISBN" value={f.isbn} onChange={e=>setF({...f,isbn:e.target.value})} required/>
      <input placeholder="Publication Year" type="number" value={f.publication_year} onChange={e=>setF({...f,publication_year:e.target.value})}/>
      <input placeholder="Copies" type="number" value={f.available_copies} onChange={e=>setF({...f,available_copies:e.target.value})}/>
      <input placeholder="Author ID" type="number" value={f.author_id} onChange={e=>setF({...f,author_id:e.target.value})} required/>
      <button className="btn btn-add" type="submit">Add</button>
    </form>
  );
}
