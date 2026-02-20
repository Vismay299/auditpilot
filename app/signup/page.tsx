import { headers } from 'next/headers'
import { redirect } from 'next/navigation'
import { createClient } from '@/lib/supabase/server'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from '@/components/ui/card'
import Link from 'next/link'

export default function SignupPage({
    searchParams,
}: {
    searchParams: { message: string }
}) {
    const signUp = async (formData: FormData) => {
        'use server'

        const origin = headers().get('origin')
        const email = formData.get('email') as string
        const password = formData.get('password') as string
        const supabase = createClient()

        const { error } = await supabase.auth.signUp({
            email,
            password,
            options: {
                emailRedirectTo: `${origin}/auth/callback`,
            },
        })

        if (error) {
            return redirect(`/signup?message=Could not authenticate user ${error.message}`)
        }

        return redirect('/login?message=Check email to continue sign in process')
    }

    return (
        <div className="flex-1 flex flex-col w-full px-8 sm:max-w-md justify-center gap-2 h-screen mx-auto">
            <Card>
                <CardHeader>
                    <CardTitle className="text-2xl">Sign up for AuditPilot</CardTitle>
                    <CardDescription>
                        Create an account to get started with automated reporting
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <form className="animate-in flex-1 flex flex-col w-full justify-center gap-2 text-foreground" action={signUp}>
                        <div className="grid gap-4">
                            <div className="grid gap-2">
                                <Label htmlFor="email">Email</Label>
                                <Input
                                    id="email"
                                    name="email"
                                    type="email"
                                    placeholder="m@example.com"
                                    required
                                />
                            </div>
                            <div className="grid gap-2">
                                <div className="flex items-center">
                                    <Label htmlFor="password">Password</Label>
                                </div>
                                <Input
                                    id="password"
                                    name="password"
                                    type="password"
                                    required
                                />
                            </div>
                            <Button type="submit" className="w-full">
                                Sign Up
                            </Button>
                            {searchParams?.message && (
                                <p className="mt-4 p-4 bg-foreground/10 text-foreground text-center text-sm">
                                    {searchParams.message}
                                </p>
                            )}
                        </div>
                    </form>
                </CardContent>
                <CardFooter>
                    <div className="text-sm text-center w-full">
                        Already have an account?{' '}
                        <Link href="/login" className="underline">
                            Log in
                        </Link>
                    </div>
                </CardFooter>
            </Card>
        </div>
    )
}
