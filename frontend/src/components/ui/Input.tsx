import * as React from "react"
import { cn } from "./utils"

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  error?: string;
  label?: string;
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, error, label, ...props }, ref) => {
    return (
      <div className="w-full space-y-1">
        {label && <label className="text-sm font-medium text-[#181925]">{label}</label>}
        <input
          type={type}
          className={cn(
            "flex h-10 w-full rounded-lg border border-[#e8e8e8] bg-white px-3 py-2 text-sm text-[#181925] transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-[#999999] focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-[#918df6] disabled:cursor-not-allowed disabled:opacity-50",
            error && "border-[#ba1a1a] focus-visible:ring-[#ba1a1a]",
            className
          )}
          ref={ref}
          {...props}
        />
        {error && <p className="text-xs text-[#ba1a1a]">{error}</p>}
      </div>
    )
  }
)
Input.displayName = "Input"

export { Input }
