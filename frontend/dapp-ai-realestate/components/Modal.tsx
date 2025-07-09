"use client"

import React, {useState} from 'react'

interface ModalProps {
    children: React.ReactNode, 
    title: string, 
    setModalOpen: React.Dispatch<React.SetStateAction<boolean>>,
}


const Modal: React.FC<ModalProps> = ({children, title, setModalOpen}) => {
  
  const closeInvestorProfileModal = (e: React.MouseEvent) => {
          setModalOpen(false);
      }
    return (
        <div className="flex flex-col gap-2 bg-white w-[70%] py-4">
          <button className="self-end w-[10%] text-red-400 bg-white text-2xl" onClick={closeInvestorProfileModal}>X</button>
          <div className="flex flex-col gap-8 items-center">
            <p className="text-2xl">{title}</p>
            {children}
          </div>
        </div>
    )
}


export default Modal;