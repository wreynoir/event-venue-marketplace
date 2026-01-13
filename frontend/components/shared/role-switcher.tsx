'use client'

import { useState } from 'react'
import { useAuthStore } from '@/lib/stores/auth-store'
import { Button } from '@/components/ui/button'

export type UserRole = 'host' | 'venue'

interface RoleSwitcherProps {
  onChange?: (role: UserRole) => void
}

export function RoleSwitcher({ onChange }: RoleSwitcherProps) {
  const { user } = useAuthStore()
  const [activeRole, setActiveRole] = useState<UserRole>('host')

  if (!user) return null

  // Only show switcher if user has both roles
  const canSwitch = user.is_host && user.is_venue_owner

  if (!canSwitch) return null

  const handleSwitch = (role: UserRole) => {
    setActiveRole(role)
    onChange?.(role)
  }

  return (
    <div className="flex items-center gap-2 p-2 bg-muted rounded-lg">
      <Button
        variant={activeRole === 'host' ? 'default' : 'ghost'}
        size="sm"
        onClick={() => handleSwitch('host')}
      >
        Host Mode
      </Button>
      <Button
        variant={activeRole === 'venue' ? 'default' : 'ghost'}
        size="sm"
        onClick={() => handleSwitch('venue')}
      >
        Venue Mode
      </Button>
    </div>
  )
}
