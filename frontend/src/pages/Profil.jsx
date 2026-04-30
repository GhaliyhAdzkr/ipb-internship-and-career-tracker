import Sidebar from "../components/SideNav";
import Navbar from "../components/NavBar";
import Test from "../components/Test";

function Profil() {
    return (
        <>
            <div className="flex bg-[#F8F9FF]">
                <Sidebar></Sidebar>
                <div className=" flex-1 flex flex-col">
                    <Navbar></Navbar>
                    <div className="flex-1 flex flex-col justify-center items-center text-3xl font-bold font-jakarta text-black">
                        <div>Profile</div>
                    </div>
                </div>
            </div>
        </>
    );
}

export default Profil;
