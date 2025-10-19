import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import api from "../../api/axiosClient";

export const fetchBooks = createAsyncThunk("books/fetchAll", async () => {
  const { data } = await api.get("/books/?skip=0&limit=100");
  return data;
});

export const createBook = createAsyncThunk("books/create", async (payload, { rejectWithValue }) => {
  try {
    const { data } = await api.post("/books/", payload); 
    return data;
  } catch (err) {
    return rejectWithValue(err.response?.data || { detail: "Create failed" });
  }
});

export const updateBook = createAsyncThunk("books/update", async ({ id, changes }, { rejectWithValue }) => {
  try {
    const { data } = await api.put(`/books/${id}`, changes); 
    return data;
  } catch (err) {
    return rejectWithValue(err.response?.data || { detail: "Update failed" });
  }
});

export const deleteBook = createAsyncThunk("books/delete", async (id, { rejectWithValue }) => {
  try {
    await api.delete(`/books/${id}`);
    return id;
  } catch (err) {
    return rejectWithValue(err.response?.data || { detail: "Delete failed" });
  }
});

const booksSlice = createSlice({
  name: "books",
  initialState: { items: [], loading: false, error: null },
  reducers: {},
  extraReducers: (builder) => {
    // fetch
    builder
      .addCase(fetchBooks.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchBooks.fulfilled, (state, action) => { state.loading = false; state.items = action.payload; })
      .addCase(fetchBooks.rejected, (state, action) => { state.loading = false; state.error = action.error.message; });

    builder.addCase(createBook.fulfilled, (state, action) => { state.items.push(action.payload); });

    builder.addCase(updateBook.fulfilled, (state, action) => {
      const i = state.items.findIndex(b => b.id === action.payload.id);
      if (i !== -1) state.items[i] = action.payload;
    });

    builder.addCase(deleteBook.fulfilled, (state, action) => {
      state.items = state.items.filter(b => b.id !== action.payload);
    });

    builder.addMatcher(
      (action) => action.type.endsWith("/rejected"),
      (state, action) => { state.error = action.payload?.detail || "Request failed"; }
    );
  }
});

export default booksSlice.reducer;
