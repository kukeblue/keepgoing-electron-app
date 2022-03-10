import { useEffect, useState } from "react";
import { createContainer } from "unstated-next"
import { TUser } from "../typing";
function useUserStore() {
    const [user, setUser] = useState<TUser>()
    useEffect(() => {
    }, [])
    return {
        user,
        setUser
    }
}

export const UserStore = createContainer(useUserStore)
