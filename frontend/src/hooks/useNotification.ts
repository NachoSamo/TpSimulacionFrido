import { toast } from "sonner";

export const useNotification = () => {
  const success = (message: string) => {
    toast.success(message, {
      style: {
        background: "#def6e4",
        color: "#33c758",
        borderColor: "#33c758",
      },
    });
  };

  const error = (message: string) => {
    toast.error(message, {
      style: {
        background: "#ffdad6",
        color: "#ba1a1a",
        borderColor: "#ba1a1a",
      },
    });
  };

  const info = (message: string) => {
    toast.info(message, {
      style: {
        background: "#dad9fc",
        color: "#918df6",
        borderColor: "#918df6",
      },
    });
  };

  return { success, error, info };
};
