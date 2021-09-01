import { useEffect, useState } from "react";
import { createContainer } from "unstated-next"
import { User } from "../typings";
function useUserStore() {
    const [user, _setUser] = useState<User | undefined>()
    useEffect(() => {
    }, [])
    const setUser = (user: User | undefined) => {
    }
    return {
        user,
        setUser
    }
}

export const UserStore = createContainer(useUserStore)
