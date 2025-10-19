import { useState } from "react";
import { useDispatch } from "react-redux";
import { updateBook } from "./booksSlice";

export default function BookFormUpdate(){
  const [id,setId]=useState("");
  const [chg,setChg]=useState({title:"",isbn:"",publication_year:"",available_copies:"",author_id:""});
  const d=useDispatch();
  const submit=e=>{
    e.preventDefault();
    const changes={
      ...(chg.title?{title:chg.title}:{}),
      ...(chg.isbn?{isbn:chg.isbn}:{}),
      ...(chg.publication_year?{publication_year:Number(chg.publication_year)}:{}),
      ...(chg.available_copies?{available_copies:Number(chg.available_copies)}:{}),
      ...(chg.author_id?{author_id:Number(chg.author_id)}:{})
    };
    d(updateBook({id:Number(id), changes}));
  };
  return (
    <form onSubmit={submit}>
      <h3>Update Book</h3>
      <input placeholder="Book ID" type="number" value={id} onChange={e=>setId(e.target.value)} required/>
      <input placeholder="New Title" value={chg.title} onChange={e=>setChg({...chg,title:e.target.value})}/>
      <input placeholder="New ISBN" value={chg.isbn} onChange={e=>setChg({...chg,isbn:e.target.value})}/>
      <input placeholder="New Year" type="number" value={chg.publication_year} onChange={e=>setChg({...chg,publication_year:e.target.value})}/>
      <input placeholder="New Copies" type="number" value={chg.available_copies} onChange={e=>setChg({...chg,available_copies:e.target.value})}/>
      <input placeholder="New Author ID" type="number" value={chg.author_id} onChange={e=>setChg({...chg,author_id:e.target.value})}/>
      <button className="btn" type="submit">Update</button>
    </form>
  );
}
