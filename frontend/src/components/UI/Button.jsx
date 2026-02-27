const Button = ({ text, icon, onClick, design }) => {
  return (
    <button onClick={onClick} className={design}> 
      {icon && <span>{icon}</span>}
      {text}
    </button>
  );
} 
export default Button;