import { useEffect, useState } from "react";
import { Button, Textarea } from "@/components";

const ChatRow = ({
  userChat,
  aiResponse,
}: {
  userChat: string;
  aiResponse: string | undefined;
}) => {
  return (
    <>
      <div className="chat chat-start">
        <div className="chat-image avatar">
          <div className="w-10 rounded-full">
            <img src="/user.png" alt="user" />
          </div>
        </div>
        <div className="chat-bubble">
          <p>{userChat}</p>
        </div>
      </div>
      {aiResponse && (
        <div className="chat chat-end">
          <div className="chat-image avatar">
            <div className="w-10 rounded-full">
              <img src="/chatbot.png" />
            </div>
          </div>
          <div className="chat-bubble">{aiResponse}</div>
        </div>
      )}
    </>
  );
};

type ChatHistoryInterface = {
  userQuery: string;
  botResponse: string;
};

const App = () => {
  const roomID = "first room";
  const [chatHistory, setChatHistory] = useState<
    ChatHistoryInterface[] | never
  >();
  const [userInput, setInput] = useState("");
  const handleSubmit = () => {
    console.log(userInput);
  };

  /* Initial data fetching */
  useEffect(() => {
    fetch(`http://localhost:8000/api/chat-history?roomID=${roomID}`)
      .then((res): Promise<{ res: ChatHistoryInterface[] }> => res.json())
      .then((returnedData) => {
        setChatHistory(returnedData?.res);
      });
  }, []);

  return (
    <>
      <div className="text-center text-5xl font-bold mt-5 mb-20">App</div>

      {/* Chat box */}
      <div className="w-[750px] mx-auto border-2 rounded-lg h-[300px] overflow-y-auto">
        {!!chatHistory &&
          chatHistory.map((chat, index) => {
            return (
              <div key={index}>
                <ChatRow
                  userChat={chat.userQuery}
                  aiResponse={chat.botResponse}
                />
              </div>
            );
          })}
      </div>

      <div className="flex flex-col items-center w-full gap-5 mt-10">
        <Textarea
          className="w-[500px]"
          value={userInput}
          onChange={(e) => setInput(e.target.value)}
        />
        <Button onClick={handleSubmit}>Submit</Button>
      </div>
    </>
  );
};

export default App;
