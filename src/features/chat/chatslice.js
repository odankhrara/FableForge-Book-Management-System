import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import api from "../../api/axiosClient";

export const fetchConversations = createAsyncThunk(
  "chat/fetchConversations",
  async (userId) => (await api.get(`/ai/conversations/?user_id=${userId}`)).data
);

export const fetchMessages = createAsyncThunk(
  "chat/fetchMessages",
  async (conversationId) => (await api.get(`/ai/messages/${conversationId}`)).data
);

export const sendMessage = createAsyncThunk(
  "chat/sendMessage",
  async ({ user_id, message, conversation_id, title }, { rejectWithValue }) => {
    try {
      const { data } = await api.post("/ai/chat/", {
        user_id,
        message,
        conversation_id,
        title,
      });
      return { conversation_id: data.conversation_id, reply: data.reply, user_msg: message };
    } catch (e) {
      return rejectWithValue(e.response?.data || { detail: "Chat failed" });
    }
  }
);

const chatSlice = createSlice({
  name: "chat",
  initialState: {
    userId: 1,                
    conversations: [],
    messagesById: {},        
    currentConversationId: null,
    sending: false,
    error: null,
  },
  reducers: {
    setCurrentConversation(state, action) {
      state.currentConversationId = action.payload; 
    },
  },
  extraReducers: (b) => {
    b.addCase(fetchConversations.fulfilled, (s, a) => {
      s.conversations = a.payload;
    });
    b.addCase(fetchMessages.fulfilled, (s, a) => {
      const { conversation_id, messages } = a.payload;
      s.messagesById[conversation_id] = messages;
      s.currentConversationId = conversation_id;
    });
    b.addCase(sendMessage.pending, (s) => {
      s.sending = true; s.error = null;
    });
    b.addCase(sendMessage.fulfilled, (s, a) => {
      s.sending = false;
      const cid = a.payload.conversation_id;
      if (!s.messagesById[cid]) s.messagesById[cid] = [];
      s.messagesById[cid].push(
        { role: "user", content: a.payload.user_msg },
        { role: "assistant", content: a.payload.reply },
      );
      if (!s.conversations.find(c => c.id === cid)) {
        s.conversations.unshift({ id: cid, user_id: s.userId, title: "New chat" });
      }
      s.currentConversationId = cid;
    });
    b.addCase(sendMessage.rejected, (s, a) => {
      s.sending = false;
      s.error = a.payload?.detail || "Chat failed";
    });
  },
});

export const { setCurrentConversation } = chatSlice.actions;
export default chatSlice.reducer;
