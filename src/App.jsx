import BooksList from "./features/books/BooksList";
import BookFormCreate from "./features/books/BookFormCreate";
import BookFormUpdate from "./features/books/BookFormUpdate";
import Chat from "./features/chat/Chat";   

export default function App() {
  return (
    <div className="container">
      <h1 className="heading">Library Frontend</h1>

      <BookFormCreate />
      <BookFormUpdate />
      <BooksList />

      <hr style={{ margin: "24px 0" }} />
      <h1 className="heading">AI Chat</h1>
      <Chat />                              
    </div>
  );
}
